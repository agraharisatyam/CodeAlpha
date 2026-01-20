from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product


def _get_cart(request: HttpRequest) -> dict[str, int]:
    cart = request.session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
        request.session["cart"] = cart
    # normalize to str->int
    normalized: dict[str, int] = {}
    for k, v in cart.items():
        try:
            normalized[str(int(k))] = max(int(v), 0)
        except (TypeError, ValueError):
            continue
    request.session["cart"] = normalized
    return normalized


def _cart_count(cart: dict[str, int]) -> int:
    return sum(cart.values())


def product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(is_active=True).order_by("name")
    cart = _get_cart(request)
    return render(
        request,
        "store/product_list.html",
        {"products": products, "cart_count": _cart_count(cart)},
    )


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = _get_cart(request)
    qty_in_cart = cart.get(str(product.pk), 0)
    return render(
        request,
        "store/product_detail.html",
        {"product": product, "qty_in_cart": qty_in_cart, "cart_count": _cart_count(cart)},
    )


@require_POST
def cart_add(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = _get_cart(request)
    key = str(product.pk)
    cart[key] = cart.get(key, 0) + 1
    request.session.modified = True
    messages.success(request, f"Added {product.name} to cart.")
    return redirect(request.POST.get("next") or "store:cart")


@require_POST
def cart_remove(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk, is_active=True)
    cart = _get_cart(request)
    key = str(product.pk)
    if key in cart:
        cart[key] = max(cart.get(key, 0) - 1, 0)
        if cart[key] == 0:
            cart.pop(key, None)
        request.session.modified = True
        messages.info(request, f"Removed 1 × {product.name}.")
    return redirect("store:cart")


def cart_view(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request)
    product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
    products = list(Product.objects.filter(id__in=product_ids, is_active=True))
    products_by_id = {p.id: p for p in products}

    items = []
    subtotal = Decimal("0.00")
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = products_by_id.get(pid)
        if not product or qty <= 0:
            continue
        line_total = product.price * qty
        subtotal += line_total
        items.append(
            {
                "product": product,
                "quantity": qty,
                "line_total": line_total,
            }
        )

    return render(
        request,
        "store/cart.html",
        {"items": items, "subtotal": subtotal, "cart_count": _cart_count(cart)},
    )


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request)
    if _cart_count(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect("store:product_list")

    product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
    products = list(Product.objects.filter(id__in=product_ids, is_active=True))
    products_by_id = {p.id: p for p in products}

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
            )

            created_any = False
            for pid_str, qty in cart.items():
                pid = int(pid_str)
                product = products_by_id.get(pid)
                if not product or qty <= 0:
                    continue
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=product.price,
                )
                created_any = True

            if not created_any:
                order.delete()
                messages.error(request, "No valid items to checkout.")
                return redirect("store:cart")

            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, f"Order #{order.pk} created.")
            return redirect("store:order_detail", pk=order.pk)
    else:
        form = CheckoutForm(
            initial={
                "full_name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        )

    subtotal = sum((products_by_id[int(pid)].price * qty for pid, qty in cart.items() if pid.isdigit() and int(pid) in products_by_id), Decimal("0.00"))
    return render(
        request,
        "store/checkout.html",
        {"form": form, "subtotal": subtotal, "cart_count": _cart_count(cart)},
    )


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("store:product_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)
            messages.success(request, "Account created. You're now logged in.")
            return redirect("store:product_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def order_detail(request: HttpRequest, pk: int) -> HttpResponse:
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk)
    if order.user_id != request.user.id:
        raise Http404()
    cart = _get_cart(request)
    return render(request, "store/order_detail.html", {"order": order, "cart_count": _cart_count(cart)})

# Create your views here.
