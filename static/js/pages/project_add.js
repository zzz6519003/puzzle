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

        $("#J_submitButton").on("click", function(){
            clickSubmitButton($(this));
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
    }

    function submitButtonClicked(actionItem){
        var data = generateFormData();
        console.log(data);
        alert();
        $.post("/project/add", {data:data}, function(returnValue){
            warningPopout(returnValue);
        }, 'json');
    }

    function deleteTime(actionItem){
        actionItem.closest(".J_mileStoneRow").slideUp("slow", function(){
            $(this).remove();
        });
    }

    function clickAddTime(actionItem){
        var milestoneHTML = $("#J_milestoneTemplate").html();
        actionItem.closest(".J_mileStoneRow").after(milestoneHTML);
        console.log(actionItem.closest(".J_mileStoneRow").html());
    }

    function clickSubmitButton(actionItem){
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

        var replacedHtml = "<label>"+selectedOption.text()+":</label>";
        datePicker.attr("data-type", selectedValue);

        actionItem.html(replacedHtml);
    }

    function generateFormData(){
        var data = [];
        $("form .J_formData").each(function(index, value){
            var dataItem = {};
            var type = $(value).attr("data-type");
            dataItem[type]=$(value).val();
            data.push(dataItem);
        });
        return data;
    }
}
