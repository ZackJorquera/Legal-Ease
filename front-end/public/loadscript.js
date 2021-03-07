window.onload = () => {
  setInterval(() => {
    fetch("http://localhost:5000/processpdf").then(req => req.text()).then(window.location.href = "http://localhost:8080/contract");
  }, 100);
}