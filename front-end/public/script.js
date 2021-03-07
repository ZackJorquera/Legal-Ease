const fileSelect = document.getElementById("fileSelect");
const fileElem = document.getElementById("fileElem");

const val = Math.floor(1000 + Math.random() * 9000);



window.onload = () => {
    function submitForm(){
	    Object.getPrototypeOf(document.getElementById("oldform")).submit.call(document.getElementById("oldform"));
      window.location.href = `http://localhost:8080/loading/${val}`;
    }
    document.getElementById('id').value = val;
    document.getElementById('fileElem').addEventListener('change', submitForm);
    fileSelect.addEventListener("click", function (e) {
    if (fileElem) {
      fileElem.click();
    }
  }, false);
};