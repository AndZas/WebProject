function initMap() {
    const myLatLng = {
        lat: 59.899962435622506, lng: 30.23457004988139
    }
    const coords1 = {
        lat: 59.85441378366863, lng: 30.108437894184338
    }
    const coords2 = {
        lat: 59.8887343012447, lng: 30.330004476999157
    }
    const coords3 = {
        lat: 59.9390844097058, lng: 30.229926829006867
    }

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: myLatLng,
    });
    addMarker(map, coords1, 'Кофейня номер 1')
    addMarker(map, coords2, 'Кофейня номер 2')
    addMarker(map, coords3, 'Кофейня номер 3')
}

function addMarker(map, coords, title) {
    new google.maps.Marker({
        position: coords,
        map,
        title: title
    })
}

window.onload = initMap