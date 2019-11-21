//just run this script on the USJ evaluation webpage (ie: Chrome DevTools Console) to select all radio buttons

var x = document.querySelectorAll('[value="Tout à fait d\'accord"]');

x.forEach(function (item, index) {
    item.checked = true;
});