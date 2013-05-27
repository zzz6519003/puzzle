pre_fix = 'controllers.'

urls = (
		"/", pre_fix + "index.Index",
		"/index", pre_fix + "index.Index",
		"/login", pre_fix + "index.Login",
		
		"/project", pre_fix + "Project.Index",
		
		"/dailyBuild", pre_fix + "DailyBuild.Index",
		
		"/aboutUs", pre_fix + "AboutUs.AboutUs",
		)
