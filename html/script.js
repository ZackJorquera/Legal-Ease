const fileSelect = document.getElementById("fileSelect");
const fileElem = document.getElementById("fileElem");

window.onload = () => {
  fileSelect.addEventListener("click", function (e) {
    if (fileElem) {
      fileElem.click();
    }
  }, false);
};