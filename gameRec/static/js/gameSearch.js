$("#search_btn").click(
  function(){
    window.location.replace("/search?keyword="
      + $("#search_text").val())
  }
);

function getQueryString(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}

function getInitPageInfo(keyword) {
  showLoadingSpinner(true);
  $.ajax({
      type:"post",
      url:"/searchInitGameLst",
      data:{"keyword":keyword},
      dataType:"json",
      success: function(data){
          console.log(data);
          refreshGameLstPage(data);
      }
  });
}

function getSelectedCheckboxes(checkBoxClassName) {
    var $checkBoxLst = $("." + checkBoxClassName);
    var retVal = new Array();
    for(var i = 0; i < $checkBoxLst.length; i++) {
      if($($checkBoxLst[i]).children("input:first").is(":checked")){
        retVal.push($($checkBoxLst[i]).attr("value"));
      }
    }
    return retVal;
}

function getPageInfo(keyword, pageIndex){
  showLoadingSpinner(true);
  var sendData = {};
  sendData['genre'] = JSON.stringify(getSelectedCheckboxes("game_search_genre_checkbox"));
  sendData['platform'] = JSON.stringify(getSelectedCheckboxes("game_search_platform_checkbox"));
  sendData['company'] = ""; //// TODO: finish compan checkbox
  sendData['keyword'] = keyword;
  sendData['pageIndex'] = pageIndex;
  $.ajax({
      type:"post",
      url:"/searchRefreshGameLst",
      data:sendData,
      dataType:"json",
      success: function(data){
          console.log(data);
          refreshGameLstPage(data);
      }
  });
}

function bindElmEvent() {
  $(".game_search_platform_checkbox")
    .children("input:first").click(
      function(){getPageInfo(getQueryString('keyword'), 0)});
  $(".game_search_genre_checkbox")
    .children("input:first").click(
      function(){getPageInfo(getQueryString('keyword'), 0)});
  //$(".game_search_company_checkbox")
  //  .children("input:first").click(
  //// TODO: Add company checkbox event
  $(".page-number").click(function(){
      getPageInfo(getQueryString('keyword'), Number($(this).attr("value")))
  });
}

function refreshGameLstPage(data){
  showLoadingSpinner(false);
  refreshCheckboxes(data.allPlatform, data.selectedPlatform, "game_search_platform_checkbox");
  refreshCheckboxes(data.allGenre, data.selectedGenre, "game_search_genre_checkbox");
  //refreshCheckboxes(data.allCompany, "game_search_company_checkbox");
  refreshGamesInfo(data.currentPageLst);
  refreshPagination($(".pagination")[0], data.currentPageIndex, data.pageCnt);
  refreshPagination($(".pagination")[1], data.currentPageIndex, data.pageCnt);
  bindElmEvent();
}

function refreshPagination(paginationDomObj, curPage, totalPage){
  var $panigation = $(paginationDomObj);
  if(totalPage == 0) {
    $panigation.hide();
  }
  else {
    $panigation.show();
  }
  if(curPage == 0){
    $panigation.children("span:first").hide();
  }
  else{
    $panigation.children("span:first").show();
    $panigation.children("span:first").attr("value", curPage - 1);
  }
  if(curPage == totalPage - 1){
    $panigation.children("span:last").hide();
  }
  else {
    $panigation.children("span:last").show();
    $panigation.children("span:last").attr("value", curPage + 1);
  }
  var elmCnt = $panigation.children("span").length;

  $($panigation.children("span")[1]).css({"background-color":"#af4aaf", "color":"white"});

  for(var i = 1; i < elmCnt - 1; i++)
  {
    if(curPage + i > totalPage)
    {
        $($panigation.children("span")[i]).hide();
    }
    else {
      $($panigation.children("span")[i]).show();
      if (i == elmCnt - 3 && curPage + i != totalPage - 1) {
          $($panigation.children("span")[i]).html("...");
          $($panigation.children("span")[i]).attr("value", totalPage - 2);
      }
      else if(i == elmCnt - 2){
          $($panigation.children("span")[i]).html(totalPage);
          $($panigation.children("span")[i]).attr("value", totalPage - 1);
      }
      else {
          $($panigation.children("span")[i]).html((curPage + i).toString());
          $($panigation.children("span")[i]).attr("value", curPage + i - 1);
      }
    }
  }
}
function refreshGamesInfo(gameLst){
  if(gameLst.length == 0) {
    $("#no_result_hint").show();
    $(".product-list:first").hide();
    return;
  }
  else {
    $("#no_result_hint").hide();
    $(".product-list:first").show();
  }
  var $list = $(".product-list");
  var $template = $list.children(".product:first");
  $template.nextAll().remove();
  for(var i = 0; i < gameLst.length; i++)
  {
      var $newOne = $template.clone(true);
      $template.after($newOne);
      $newOne.children(".inner-product").find("a:first").attr("href", gameLst[i].gameUrl);
      $newOne.children(".inner-product").find("img:first").attr("src", gameLst[i].imageUrl);
      $newOne.find(".product-title:first").children("a:first").html(gameLst[i].title);
      $newOne.find(".product-title").children("a:first").attr("href", gameLst[i].gameUrl);
      $newOne.find(".platform").html(gameLst[i].platform);
      $newOne.find(".genre").html(gameLst[i].genre);
      $newOne.find(".game_desc").html(gameLst[i].description);
  }
  $template.remove()

}

function refreshCheckboxes(names, selectedNames, className){
  var $template = $('.' + className + ':first');
  $template.nextAll().remove();
  names.forEach(function(item, index, arr){
    var $newOne = $template.clone(true);
    $template.after($newOne);
    $newOne.children("label:first").html(item);
    $newOne.attr("value", item);
    $newOne.children("input:first").prop("checked", selectedNames.includes(item));

    //$("#cb1").prop("checked",true);
  });
  $template.remove();
}

var spinner = new Spin.Spinner({radius: 30,top: '50%',left: '50%'});
function showLoadingSpinner(show){
  if(show) {
    $(".fullscreen:first").show();
    spinner.spin($("#search_spinner").get(0));
    $("body:first").css("overflow:hidden");
  }
  else {
    $(".fullscreen:first").hide();
    spinner.spin();
    $("body:first").css("overflow:visible");
  }
}
