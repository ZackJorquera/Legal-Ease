const fileSelect = document.getElementById("fileSelect");
const fileElem = document.getElementById("fileElem");

const handleChange = () => {
  document.getElementById('upload').submit();
  window.location.href = "http://localhost:8080/loading";
}

window.onload = () => {
  fileSelect.addEventListener("click", function (e) {
    if (fileElem) {
      fileElem.click();
    }
  }, false);
};