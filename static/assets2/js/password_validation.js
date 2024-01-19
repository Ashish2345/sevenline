$(".checkicon").hide();
const passRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/

const pass2 = document.getElementById("pass2");
const pass1 = document.getElementById("pass1");

function togglePassword(x, icon) {
  if (x.type === "password") {
    x.type = "text";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  } else {
    x.type = "password";
    icon.classList.add("fa-eye-slash");
    icon.classList.remove("fa-eye");
  }
}



$("#pass2").click(function () {
  togglePassword(id_password2, pass2);
});
function addMeClass(divid, classes) {
  $(`#${divid}`).addClass(`${classes}`);
  $(`#${divid}`).find("i").show();
}
function removeMeClass(divid, classes) {
  $(`#${divid}`).removeClass(`${classes}`);
  $(`#${divid}`).find("i").hide();
}

  let myInput = document.getElementById("id_password1");
  let myInput2 = document.getElementById("id_password2");
  myInput.onkeyup = function () {

  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if (myInput.value.match(lowerCaseLetters)) {
      addMeClass("lower_letter", "greentext");
  } else {
      removeMeClass("lower_letter", "greentext");
  
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if (myInput.value.match(upperCaseLetters)) {
      addMeClass("capital_letter", "greentext");
  } else {
      removeMeClass("capital_letter", "greentext");
  
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if (myInput.value.match(numbers)) {
      addMeClass("number_text", "greentext");
  } else {
      removeMeClass("number_text", "greentext");
  
  }

  // Validate length
  if (myInput.value.length >= 8) {
      addMeClass("eight_char", "greentext");
  } else {
      removeMeClass("eight_char", "greentext");
  
  }

  var special = /([-+=_!@#$%^&*.,;:'\"<>/?`~\[\]\(\)\{\}\\\|\s])/;
  if (myInput.value.match(special)) {
      addMeClass("special_char", "greentext");
  } else {
      removeMeClass("special_char", "greentext");
  
  }
  if (myInput.value.length < 8) {
      $("#id_password2").prop("disabled", true);
  } else {
      $("#id_password2").prop("disabled", false);
  }
  
  };
  if (myInput.value.length < 8) {
      $("#id_password2").prop("disabled", true);
  }

  
  $("#repassword-fail").hide();
  $("#repassword-pass").hide();
  
  const id_password2 = document.getElementById("id_password2");
  $("#submit_password").prop("disabled", true);
  id_password2.onkeyup = function () {
      if (id_password2.value !== myInput.value) {
      $("#repassword-fail").show();
      $("#repassword-pass").hide();
     

      } else {
      $("#repassword-pass").show();
      $("#repassword-fail").hide();
      $('#submit_password').removeAttr('disabled');
      }
  };