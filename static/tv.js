
// TV Shows
currentPage = 1
totalPages = 1

function addTVs(currentPage) {
    url_tv = `https://api.themoviedb.org/3/discover/tv?` + 
            `api_key=${'daa7c37e8875b873c494c4070f234516'}` +
            `&page=${currentPage}` +
            `&region=${session['watch_region']}` + 
            `&with_original_language=${session['target_language']}` + 
            `&with_watch_monetization_types=flatrate|free|ads|rent|buy`

    fetch(url_tv)
    .then((response) => response.json())
    .then((data) => {
        totalPages = data['total_pages']
        data.results.forEach(tv => {
            newTV = `<a href="/tv-details?id=${tv['id']}" class="hover:scale-105 ease-in-out duration-300">
                            <img class="rounded-t h-72 w-full object-cover" src="https://image.tmdb.org/t/p/w500/${tv['poster_path']}" alt="${tv['name']}">
                            <p>${tv['name']} <span class="text-sm opacity-80">(${tv['first_air_date'].split('-')[0]})</span></p>
                        </a>`
            document.getElementById(`section-tv`).innerHTML += newTV
        })
    })
}

document.getElementById('more-tv').addEventListener('click', () => {
    currentPage += 1
    if (currentPage < totalPages) {
        addTVs(currentPage)
    }
    if (currentPage === totalPages) {
        document.getElementById('more-tv').classList.add('hidden')
    }
})

addTVs(1)