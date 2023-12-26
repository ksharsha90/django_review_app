from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, "home.html",
                  {"searchTerm": searchTerm, 'movies': movies})


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    context = {
        "movie": movie,
        "reviews": reviews
    }
    return render(request, "detail.html", context)


@login_required
def review_create_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "GET":
        return render(request, 'createreview.html', {'form': ReviewForm(),
                                                     'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form': ReviewForm(),
                                        'error': "bad data is passed In"})

@login_required

def review_update_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == "GET":
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review,
                                                     'form': form})
    else:
        try:
            form = ReviewForm(request.POST,
                              instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            form = ReviewForm(request.POST,
                              instance=review)
            return render(request, 'updatereview.html', {'review': review,
                                                         'form': form,
                                                         'error': "Bad data in form"})


@login_required
def review_delete_view(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)


def about(request):
    return HttpResponse("<h1>About us Page</h1>")


