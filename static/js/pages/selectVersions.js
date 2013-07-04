$(document).ready(function(){
    var selectVersion = new SelectVersion();
    selectVersion.init();
});

function SelectVersion()
{
    var body = $("body");

    this.init = function(){
        bindEvent();
    };

    function bindEvent(){
        body.on("click", ".J_versionBadge", function(){
            versionBadgeClicked($(this));
        });

        body.on("click", "#J_packageButton", function(){
            packageButtonClicked($(this));
        });
    }

    function packageButtonClicked(actionItem){
        var data = getDependencySha1();
        $.post("/packageBuild/buildPackage", {data:JSON.stringify(data)}).done(function(){
            //self.location = "/";
        });
        warningPopout("打包功能还没写呢");
    }

    function versionBadgeClicked(actionItem){
        actionItem.siblings(".J_versionBadge").removeClass("badge-success");
        actionItem.addClass("badge-success");
    }

    function getDependencySha1(){
        var data={};

        $(".J_versionBadge.badge-success").each(function(index, value){
            var item = $(value);
            var repoId = item.context.dataset['repoId'];
            var sha1 = item.context.dataset['sha1'];
            data[repoId] = sha1;
        });

        return data;
    } 
}
