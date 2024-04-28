document.addEventListener("DOMContentLoaded", function () {
    const photos = document.querySelectorAll(".photo");

    photos.forEach(function (photo) {
        photo.addEventListener("click", function () {
            const info = this.querySelector(".info");
            const title = this.querySelector("h3").textContent;
            const date = info.querySelector("p:nth-child(2)").textContent;
            const genre = info.querySelector("p:nth-child(3)").textContent;
            const emotions = info.querySelector("p:nth-child(4)").textContent;

            document.getElementById("popup-title").textContent = title;
            document.getElementById("popup-date").textContent = date;
            document.getElementById("popup-genre").textContent = genre;
            document.getElementById("popup-emotions").textContent = emotions;

            document.getElementById("popup").style.display = "block";
        });
    });

    document.querySelector(".close").addEventListener("click", function () {
        document.getElementById("popup").style.display = "none";
    });
});
