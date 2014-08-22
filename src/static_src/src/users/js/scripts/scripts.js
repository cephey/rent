document.getElementById("previewImg").addEventListener("click", function () {
    document.querySelector("input[type=file]").click();
}, false);

if (window.File && window.FileReader && window.FileList && window.Blob) {

    document.querySelector("input[type=file]").addEventListener("change", function (e) {
        var place = document.getElementById("previewImg");
        var f = e.target.files[0];

        var reader = new FileReader;
        reader.readAsDataURL(f);
        reader.onload = function (e) {
            place.src = e.target.result;
        }
    }, false);

} else {
    console.warn("Ваш браузер не поддерживает FileAPI");
}