$(document).ready(function(){
    var addProject = new AddProject();
    addProject.init();
});

function AddProject()
{
    var body = $("body");

    this.init = function(){
        bindEvent();
    }

    function bindEvent(){

        body.on("click", ".J_addTime", function(){
            clickAddTime($(this));
        });

        body.on("click", ".J_delTime", function(){
            if($("form .J_mileStoneRow").length > 1){
                deleteTime($(this));
            }else{
                warningPopout("别赶尽杀绝啊，留一条生路嘛。");
            }
        });

        body.on("focusin", ".J_pickTime", function(){
            $(this).datepicker({
                dateFormat:"yy-mm-dd",
                inline:true
            });
        });

        body.on("mouseenter", ".J_timeRow", function(){
            hoverInTimePicker($(this));
        });

        body.on("mouseleave", ".J_timeRow", function(){
            hoverOutTimePicker($(this));
        });

        body.on("click", ".J_selectMileStone", function(){
            if($(this).children("label").length > 0){
                switchMilestoneToSelector($(this));
            }
        });

        body.on("mouseleave", ".J_selectMileStone", function(){
            if($(this).children("select").length > 0){
                switchSelectorToMilestone($(this));
            }
        });

        $("#J_submitButton").on("click", function(){
            submitButtonClicked($(this));
        });

        body.on("click", "input", function(){
            $(this).closest(".control-group").removeClass("error");
        });
    }

    function submitButtonClicked(actionItem){
        if(isAvailable()){
            var data = generateFormData();
            $.post("/project/add", data).done(function(){
                window.location.href="/project";
            });
        }
    }

    function deleteTime(actionItem){
        actionItem.closest(".J_mileStoneRow").slideUp("slow", function(){
            $(this).remove();
        });
    }

    function clickAddTime(actionItem){
        var milestoneHTML = $("#J_milestoneTemplate").html();
        actionItem.closest(".J_mileStoneRow").after(milestoneHTML);
    }

    function hoverInTimePicker(actionItem){
        actionItem.children(".J_operations").removeClass("hide");
    }

    function hoverOutTimePicker(actionItem){
        actionItem.children(".J_operations").addClass("hide");
    }

    function switchMilestoneToSelector(actionItem){
        var selectorHtml = $("#J_selectorTemplate").html();
        actionItem.html(selectorHtml);
    }

    function switchSelectorToMilestone(actionItem){
        var selector = actionItem.children("select");
        var datePicker = actionItem.closest(".J_mileStoneRow").find(".J_pickTime");

        var selectedValue = selector.val();
        var selectedOption = actionItem.find("option:selected");

        var replacedHtml = "<label><font color=\"pink\">"+selectedOption.text()+":</font></label>";
        datePicker.attr("data-type", selectedValue);

        actionItem.html(replacedHtml);
    }

    function generateFormData(){
        var data = {};
        $("form .J_formData").each(function(index, value){
            var type = $(value).attr("data-type");
            var value = $(value).val();

            data[type] = value;
        });
        return data;
    }

    function isAvailable(data){
        var result = true;

        $("form .control-group").each(function(index, value){
            item = $(value);
            formData = item.find(".J_formData");

            if(typeof formData.val() != "undefined"){
                if(formData.val().length == 0){
                    item.addClass('error');
                    result = false;
                }
            }
        });

        return result;
    }
}
