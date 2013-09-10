(function(){
    var release = new Release();
    release.init();
})();

function Release(){
    var body = $("body");

    this.init = function(){
        bindEvent();
    }

    function bindEvent(){
        body.on("click", "#J_RTreleaseButton", function(){
            releaseButtonClicked($(this));
        });

        body.on("click", "#J_RTchannelButton", function(){
            channelButtonClicked($(this));
        })
    }

    function channelButtonClicked(actionItem){
        var projectId = actionItem.context.dataset['projectId'];
        var category = actionItem.context.dataset['category'];
        gotoSelectVersion(actionItem);
    }

    function releaseButtonClicked(actionItem){
        var projectId = actionItem.context.dataset['projectId'];
        var category = actionItem.context.dataset['category'];
        gotoSelectVersion(actionItem);
    }
}


