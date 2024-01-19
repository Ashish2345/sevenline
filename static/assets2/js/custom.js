var otp_inputs = document.querySelectorAll(".otp__digit")
console.log(otp_inputs)
var mykey = "0123456789".split("")
otp_inputs.forEach((_)=>{
  _.addEventListener("paste", handle_paste_input)
  _.addEventListener("keyup", handle_next_input)
 
})


function handle_paste_input(event) {
  let current = event.target;
  let pasteData = (event.clipboardData || window.clipboardData).getData('text');

  for (let i = 0; i < pasteData.length; i++) {
    if (i >= 6 || parseInt(current.classList[1].split("__")[2]) + i > 6) break;
    let index = parseInt(current.classList[1].split("__")[2]) + i;
    if (mykey.indexOf(pasteData[i]) != -1) {
      otp_inputs[index - 1].value = pasteData[i];
      if (index < 6) {
        otp_inputs[index].focus();
      }
    }
  }

  event.preventDefault();
}

function handle_next_input(event){
  let current = event.target
  let index = parseInt(current.classList[1].split("__")[2])

  if (mykey.indexOf(""+event.key+"") != -1) {
    current.value = event.key;
    
    if(index < 6){
      var next = current.nextElementSibling;
      next.focus()
    }
  }
  else if(event.keyCode == 8 && index > 1){
    current.value = "";
    current.previousElementSibling.focus()
  }
}
