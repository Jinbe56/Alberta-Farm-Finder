from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from farms.models import Farm
from .models import Review


def review_list(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    reviews = farm.reviews.select_related('author').all()
    return render(request, 'reviews/_list.html', {
        'farm': farm,
        'reviews': reviews,
    })


@login_required
def review_create(request, slug):
    farm = get_object_or_404(Farm, slug=slug)

    if farm.owner == request.user:
        return render(request, 'reviews/_list.html', {
            'farm': farm,
            'reviews': farm.reviews.select_related('author').all(),
            'error': "You can't review your own farm.",
        })

    if Review.objects.filter(farm=farm, author=request.user).exists():
        return render(request, 'reviews/_list.html', {
            'farm': farm,
            'reviews': farm.reviews.select_related('author').all(),
            'error': "You've already reviewed this farm.",
        })

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        text = request.POST.get('text', '').strip()
        if 1 <= rating <= 5 and text:
            Review.objects.create(
                farm=farm,
                author=request.user,
                rating=rating,
                text=text,
            )

    reviews = farm.reviews.select_related('author').all()
    return render(request, 'reviews/_list.html', {
        'farm': farm,
        'reviews': reviews,
    })


@login_required
def review_respond(request, slug, pk):
    farm = get_object_or_404(Farm, slug=slug)
    if farm.owner != request.user:
        return redirect('farms:detail', slug=slug)

    review = get_object_or_404(Review, pk=pk, farm=farm)
    if request.method == 'POST':
        response_text = request.POST.get('response', '').strip()
        if response_text:
            review.farmer_response = response_text
            review.farmer_responded_at = timezone.now()
            review.save()

    return redirect('farms:detail', slug=slug)
