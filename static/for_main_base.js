function toggleProfilePanel() {
    var username = document.getElementsByClassName('username_class')[0];
    var panel = document.getElementsByClassName('nav ul li')[0];
    if (panel.style.display === 'none') {
        panel.style.display = 'block'
    } else {
        panel.style.display = 'none'
    }
    if (username.style.color === 'black') {
        username.style.color = '#00754A'
    } else {
        username.style.color = 'black'
    }
}