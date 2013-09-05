/**
 * Created with PyCharm.
 * User: yuetingqian
 * Date: 13-8-30
 * Time: 下午3:29
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(
    function () {
        lastweek = 7 * 24 * 60 * 60;

        Highcharts.theme = {
            colors: ['#4572a7', '#c0c0c0', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],

            title: {
                style: {
                    color: '#000',
                    font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
                }
            },
            subtitle: {
                style: {
                    color: '#666666',
                    font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
                }
            },

            legend: {
                itemStyle: {
                    font: '9pt Trebuchet MS, Verdana, sans-serif',
                    color: 'black'
                },
                itemHoverStyle: {
                    color: 'gray'
                }
            }
        };

        Highcharts.setOptions(Highcharts.theme);


        var options = {
            chart: {
                type: 'spline',
                renderTo: 'container'
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Crash Count'
            },

            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }

            },
            yAxis: {
                title: {
                    text: 'Count'
                },
                min: 0
            },
            tooltip: {
                crosshairs: true,
                formatter: function () {
                    if (this.series.name == 'lastweek') {
                        this.x = this.x / 1000 - lastweek;
                        this.x = timestampToUTC(this.x);
                    }
                    html = Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x);
                    html += '<br>' + this.series.name + '：' +
                        '<span style="font-weight:bold;color:' + this.series.color + '">' +
                        this.y + '</span>';
                    return html;
                },
                valueSuffix: '个'
            },
            plotOptions: {
                spline: {
                    lineWidth: 2,
                    states: {
                        hover: {
                            lineWidth: 3
                        }
                    },
                    marker: {
                        enabled: false,
                        states: {
                            hover: {
                                enabled: true,
                                radius: 4
                            }
                        }
                    },
                    pointInterval: 3600000 // one hour
//                    pointStart: Date.UTC(2013, 8, 1, 0, 0, 0)
                }
            },
            series: [
                {
                    name: 'today'
                },
                {
                    name: 'lastweek'
                }

            ]
        };
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        $('#dt_date').change(function () {
            $('#dt_start').val($('#dt_date').val());
            $('#dt_end').val($('#dt_date').val());
        });

        dt_start = $('#dt_start').val();
        dt_end = $('#dt_end').val();
        dt_start_obj = $.datepicker.parseDate('yy-mm-dd', dt_start);
        dt_end_obj = $.datepicker.parseDate('yy-mm-dd', dt_end);
        param = getParams();
        getData(param, options);

        $('.J_pickTime.J_formData').datepicker({
            dateFormat: "yy-mm-dd",
            inline: true
        });
        $('#btn_submit').click(function () {
                setDtDate();
                try {
                    param = getParams();
                    getData(param, options);
                } catch (err) {
                    alert('日期不正确');
                    return false;
                }
            }
        );


        $('#btngrp_date_range :button').click(function () {

            if ($(this).attr('dt_date')) {
                $('#dt_start, #dt_end').val($(this).attr('dt_date'));
            } else {
                $('#dt_start').val($(this).attr('dt_start'));
                var mytime = getCurrentDate()
                $('#dt_end').val(mytime);
            }

            dt_start = $('#dt_start').val();
            dt_end = $('#dt_end').val();
            dt_start_obj = $.datepicker.parseDate('yy-mm-dd', dt_start);
            dt_end_obj = $.datepicker.parseDate('yy-mm-dd', dt_end);
            setDtDate();
            param =getParams();
            getData(param, options);
        });

    }


);
function getCurrentDate() {
    var myDate = new Date();
    var year = myDate.getFullYear();
    var month = myDate.getMonth() + 1;
    var day = myDate.getDate();
    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day;
    }
    var mytime = year + '-' + month + '-' + day;
    return mytime;
}

function timestampToUTC(timestamp) {
    timestamp = timestamp - 8 * 60 * 60;
    var d = new Date(timestamp * 1000);
    jstimestamp = Date.UTC(d.getFullYear(), d.getMonth(), d.getDate(), d.getHours(), d.getMinutes(), d.getSeconds());
    var date = d.getFullYear() + '  ' + d.getMonth() + '  ' + d.getDate() + '  ' + d.getHours() + '  ' + d.getMinutes();
    return jstimestamp;
}


function getData(params, options) {
    url = "/monitor/getdata"

    $.getJSON(url, params, function (data) {
        for (i in data) {
            for (j in data[i]) {
                if (i == 0) {
                    data[i][j][0] = timestampToUTC(data[i][j][0]);
                } else {
                    data[i][j][0] = getLastWeek(data[i][j][0]);
                }
            }
        }

        options.series[0].data = data[0];
        options.series[1].data = data[1];
        var chart = new Highcharts.Chart(options);
        // setMinMax();
    });
}


function setDtDate() {
    if ($('#dt_start').val() == $('#dt_end').val()) {
        $('#dt_date').val($('#dt_start').val());
    } else {
        $('#dt_date').val('');
    }
}
function getLastWeek(timestamp) {
    var time = timestamp + lastweek;
    time = timestampToUTC(time);
    return time;
}
function getParams() {
    dt_start = $('#dt_start').val();
    dt_end = $('#dt_end').val();
    dt_start_obj = $.datepicker.parseDate('yy-mm-dd', dt_start);
    dt_end_obj = $.datepicker.parseDate('yy-mm-dd', dt_end);
    app_name = $('#app_name').val();
    app_platform = $('#app_platform').val();
    param = 'app_name=' + app_name + '&app_platform=' + app_platform + '&start=' + dt_start + '&end=' + dt_end;
    return param;
}