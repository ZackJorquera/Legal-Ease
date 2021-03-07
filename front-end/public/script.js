const fileSelect = document.getElementById("fileSelect");
const fileElem = document.getElementById("fileElem");

const val = Math.floor(1000 + Math.random() * 9000);

const handleChange = () => {
  document.getElementById('upload').submit();
  window.location.href = `http://localhost:8080/loading/${val}`;
}



window.onload = () => {
  document.getElementById('id').value = val;

  fileElem.addEventListener('change', function(e) {
    handleChange();
  });

  fileSelect.addEventListener("click", function (e) {
    if (fileElem) {
      fileElem.click();
    }
  }, false);
};