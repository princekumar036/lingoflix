
// TV SHOWS
let tv_pageNo_el = document.getElementById('tv-pageNo')
let tv_pageNo = parseInt(tv_pageNo_el.value)
let tv_form = document.getElementById('tv-form')

tv_form.addEventListener('submit', function(e) {
    e.preventDefault()

    tv_pageNo += 1
    if (tv_pageNo === total_pages) {
        tv_form.classList.add('hidden')
        return
    }
    tv_pageNo_el.setAttribute('value', tv_pageNo)
    const formData = new FormData(tv_form)

    fetch('/tv', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        data.forEach(tv => {
            newTV = `<a href="/tv-details?id=${tv['id']}" class="hover:scale-105 ease-in-out duration-300">
                            <img class="rounded-t h-72 w-full object-cover" src="https://image.tmdb.org/t/p/w185${tv['poster_path']}" alt="${tv['name']}">
                            <p>${tv['name']} <span class="text-sm opacity-80">(${tv['first_air_date'].split('-')[0]})</span></p>
                        </a>`
            document.getElementById('tv-section').innerHTML += newTV
        })
    })
})