//记录时间给别的脚本用
var date = new Date();
//你妹！js计算月份是从0开始算的！
var today = date.getFullYear() + '/' + (date.getMonth()+1) + '/' + date.getDate();
var timestamp = Date.parse(today)/1000;

$(document).ready(function(){
    var mainPage = new MainPage();
    mainPage.init();
});

function MainPage(){

    var body = $("body");

    this.init = function(){
        bindEvent();
    };

    function bindEvent(){
        body.on("click", "#J_setupButton", function(){
            setupButtonClicked($(this));
        });
    }

    function setupButtonClicked(actionItem){
        var contentHtml = $("#J_templateSetup").html();
        var username = "";
        var projectPath = "";
    
        if(typeof($.cookie("puzzleUsername")) != "undefined" && typeof($.cookie("puzzleProjectPath")) != "undefined"){
            username = $.cookie("puzzleUsername");
            projectPath = $.cookie("puzzleProjectPath");
        }
    
        contentHtml = contentHtml.replace(/__username__/g, username);
        contentHtml = contentHtml.replace(/__projectPath__/g, projectPath);
    
        $.colorbox({
            html:contentHtml,
            onCleanup:function(){
                var username = $("#cboxContent #J_setupUsername").val();
                var projectPath = $("#cboxContent #J_setupProjectPath").val();
    
                if(username != '' && projectPath != ''){
                    $.cookie('puzzleUsername', username, {expires:365});
                    $.cookie('puzzleProjectPath', projectPath, {expires:365});
                }
            }
        });
    }
}
