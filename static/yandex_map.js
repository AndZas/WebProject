ymaps.ready(init);

function init() {
    var currentPage = window.location.pathname;
    if (currentPage === '/address') {
        center = [59.945752, 30.382842]
        zoom = 10
    } else if (currentPage === '/myprofile') {
        center = [55, 34]
        zoom = 17
    }

    var geolocation = ymaps.geolocation, myMap = new ymaps.Map('map', {
        center: center, zoom: zoom
    }, {
        searchControlProvider: 'yandex#search'
    });


    if (currentPage === '/address') {
        let lst = [[60.010987, 30.400480], [59.919581, 30.465348], [59.877127, 30.358888]]
        for (i = 0; i < 3; i++) {
            var myPlacemark = new ymaps.Placemark(lst[i], { // координаты метки
                hintContent: 'Москва', // подсказка при наведении на метку
                balloonContent: 'Столица России' // контент во всплывающем окне метки
            });
            myMap.geoObjects.add(myPlacemark);
        }
    } else if (currentPage === '/myprofile') {
        geolocation.get({
            provider: 'browser', mapStateAutoApply: true
        }).then(function (result) {
            // Синим цветом пометим положение, полученное через браузер.
            // Если браузер не поддерживает эту функциональность, метка не будет добавлена на карту.
            result.geoObjects.options.set('preset', 'islands#blueCircleIcon');
            myMap.geoObjects.add(result.geoObjects);
        })
    }
}