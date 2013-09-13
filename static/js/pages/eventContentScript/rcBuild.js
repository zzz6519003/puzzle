(function(){
    var body = $("body");

    body.on("click", "#J_rcBuildButton", function(){
        rcBuildButtonClicked($(this));
    });
})();

function rcBuildButtonClicked(actionItem){
    $.colorbox({
        html:'<img src="/static/img/ajax-loader.gif">',
        overlayClose:false,
        escKey:false,
        closeButton:false,
        onLoad:function(){
            $('#cboxClose').remove();
        },
        onComplete:function(){
            gotoSelectVersion(actionItem);
        }
    });
}
