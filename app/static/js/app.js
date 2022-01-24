// document elements
const menu_btn = document.querySelector(".menu_toggle");
const menu = document.querySelector(".nav_bar");

const emailField = document.querySelector("#email");
const passwordField = document.querySelector("#password");
const passwordField2 = document.querySelector("#password2")

// Register event handlers
menu_btn.addEventListener("click", openMenu);

emailField.addEventListener("keypress", emailValidate);
passwordField.addEventListener("keyup", passwordValidate);

if(passwordField2 !== null){
  passwordField2.addEventListener("keyup", confirmPassword);
}



// custom functions
function openMenu() {
  menu.classList.toggle("open_nav");
}

window.setInterval(clearError, 2000);

function clearError() {

  let error_message = document.querySelector(".notification");

  if(error_message != null){
    error_message.classList.add('clear_notification')
  }

  
}

// email validator

function emailValidate() {
  let emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  // if the value of this field does not match the pattern then notify with an error message
  // otherwise notify with a success message

  if (!this.value.match(emailRegex)) {
    notify(this, message = "Invalid Email", state = "error");
  } else {
    notify(this, message = "",state = "success");
  }
}
// password validation
function passwordValidate() {
  let passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;

  // if the value of the field does not match the regix pattern then notify with an error
  // otherwise notify with a success message

  if (!this.value.match(passwordRegex)) {
    notify(this, message = "Invalid password", state = "error");
  } else {
    notify(this, message = "",state = "success");
  }
}

function confirmPassword() {

  if(this.value != passwordField.value){
    notify(this, message = "Password don't  match", state = "error");
    return
  }
  else{
    
    notify(this, message = "",state = "success");
  }
  
  
}
// user notification function

function notify(element, message = "", state) {

  let errorMessageElement = element.nextElementSibling;
  let successIndicator = element.previousElementSibling.previousElementSibling.previousElementSibling;
  let errorIndicator = element.previousElementSibling.previousElementSibling;

  switch (state) {
    case "success":

        // check if the elements had an error state applied to them first
        if(element.classList.contains('error')){
            element.classList.remove('error')
            errorIndicator.classList.remove('indicate')
        }
        element.classList.add('success')
        successIndicator.classList.add('indicate')
      break;
    case "error":
        if(element.classList.contains('success')){
            element.classList.remove('success')
            successIndicator.classList.remove('indicate')
        }
        element.classList.add('error')
        errorIndicator.classList.add('indicate')
      break;

    default:
      break;
  }
}
