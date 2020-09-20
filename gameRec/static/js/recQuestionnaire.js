selGenreSet = new Set();
selPlatformSet = new Set();

function submitQuestionnaire (url, arg) {
  var form = $("<form method='post'></form>");
  form.attr({"action":url});
  var input = $("<input type='hidden'>");
  input.attr({"name":"questionnaireJsonInfo"});
  input.val(JSON.stringify(arg));
  form.append(input);
  $(document.body).append(form);
  form.submit();
}

function addSelInfo(type, val) {
  if(type == "genre") {

      selGenreSet.add(val);

  }
  else if (type == "platform") {

      selPlatformSet.add(val);
  }
}
function rmvSelInfo(type, val) {
  if(type == "genre") {
      selGenreSet.delete(val);

  }
  else if (type == "platform") {

      selPlatformSet.delete(val);

  }
}

function onClickQuestionnaireItem() {
  var selected = this.getAttribute("haveSelected");
  if(selected != undefined && selected == "sel"){
      this.setAttribute("style", "background:#ffffff");
      this.setAttribute("haveSelected", "unsel");
      rmvSelInfo(this.getAttribute("type"), this.getAttribute("value"));
  }
  else {
      this.setAttribute("style", "background:#69c697");
      this.setAttribute("haveSelected", "sel");
      addSelInfo(this.getAttribute("type"), this.getAttribute("value"));
  }
  console.log(selGenreSet);
  console.log(selPlatformSet);

}

function onClickSubmit() {
  submitQuestionnaire(this.getAttribute("url"),
    {"selGenreSet":(Array.from(selGenreSet)), "selPlatformSet":(Array.from(selPlatformSet))});
}

function initQuestionnairePage(){
  $(".questionnaire_selitem").click (onClickQuestionnaireItem);
  $("#submitBtn").click(onClickSubmit)
}
