pre_fix = 'controllers.'

urls = (
        "/", pre_fix + "index.Index",
        "/index", pre_fix + "index.Index",
        "/login", pre_fix + "index.Login",
        
        "/project", pre_fix + "Project.Index",
        "/project/add", pre_fix + "Project.Add",

        "/dailyBuild", pre_fix + "DailyBuild.Index",
        
        "/aboutUs", pre_fix + "AboutUs.AboutUs",

        "/timeline", pre_fix + "TimeLine.Index",
        
        "/clipAdd", pre_fix + "UiClipper.clipAdd",
        "/addPicture", pre_fix + "UiClipper.addPicture",
        "/mobileUi", pre_fix + "UiClipper.mobileUi",

        "/packageBuild/ajaxCheckNewVersion", pre_fix + "PackageBuild.AjaxCheckNewVersion",
        "/packageBuild/selectVersions", pre_fix + "PackageBuild.SelectVersions",
        "/packageBuild/buildPackage", pre_fix + "PackageBuild.BuildPackage",
        )
