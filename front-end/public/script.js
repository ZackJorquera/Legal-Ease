const fileSelect = document.getElementById("fileSelect");
const fileElem = document.getElementById("fileElem");

const handleChange = () => {
  document.getElementById('upload').submit();
}

window.onload = () => {
  fileSelect.addEventListener("click", function (e) {
    if (fileElem) {
      fileElem.click();
    }
  }, false);
};