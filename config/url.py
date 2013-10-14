pre_fix = 'controllers.'

urls = (
        "/", pre_fix + "index.Index",

        "/index", pre_fix + "index.Index",
        "/login", pre_fix + "index.Login",

        "/startGearman", pre_fix + "BackGround.StartGearman",
        "/gearmanWorkers", pre_fix + "BackGround.GearmanWorkers",
        "/gearmanStatus", pre_fix + "BackGround.GearmanStatus",

        "/project", pre_fix + "Project.Index",
        "/project/add", pre_fix + "Project.Add",
        "/project/del", pre_fix + "Project.Del",
        "/project/initScript", pre_fix + "Project.InitScript",

        "/dailyBuild", pre_fix + "DailyBuild.Index",

        "/aboutUs", pre_fix + "AboutUs.AboutUs",

        "/appStore", pre_fix + "AppStore.Index",

        "/timeline", pre_fix + "TimeLine.Index",

        "/clipAdd", pre_fix + "UiClipper.clipAdd",
        "/addPicture", pre_fix + "UiClipper.addPicture",
        "/mobileUi", pre_fix + "UiClipper.mobileUi",

        "/packageBuild/ajaxCheckNewVersion", pre_fix + "PackageBuild.AjaxCheckNewVersion",
        "/packageBuild/selectVersions", pre_fix + "PackageBuild.SelectVersions",
        "/packageBuild/buildPackage", pre_fix + "PackageBuild.BuildPackage",
        "/packageBuild/inputCommit", pre_fix + "PackageBuild.InputCommit",
        "/packageBuild/copyProject", pre_fix + "PackageBuild.CopyProject",

        "/showCmdLog", pre_fix + "BuildProgress.ShowCmdLog",
        "/progressNumber", pre_fix + "BuildProgress.ProgressNumber",
        "/initProjectProgress", pre_fix + "BuildProgress.InitProjectProgressBar",

        "/report/update" , pre_fix +"Report.Update",
        "/report/index",pre_fix + "Report.Index",
        "/report/reason",pre_fix + "Report.Reason",
        "/report/component",pre_fix + "Report.Component",
        "/report/developer", pre_fix + "Report.Developer",
        "/report/qa",pre_fix + "Report.Qa",
        "/report/detail",pre_fix + "Report.Detail",
        "/report/job",pre_fix + "Report.Job",

        "/crash/job", pre_fix + "Crash.Job",
        "/crash/set", pre_fix + "Crash.Set",

        "/monitor/getdata", pre_fix + "Monitor.GetData",
        "/monitor/detail", pre_fix + "Monitor.Detail",
        "/monitor/chartlist", pre_fix + "Monitor.ChartList",

        "/notification/gitcorpDidMergePullRequest", pre_fix + "NotificationCenter.GitCorpDidMergePullRequest",
        )
