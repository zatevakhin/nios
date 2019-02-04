"use strict";

let EServiceType = Object.freeze({
    1: "Router",
    2: "Nas",
    3: "Dvr",
    4: "Server",
    5: "Unknown"
})



class CScanner
{
    constructor()
    {

    }

    getStatistics()
    {
        $.post('/statistics')
            .done((data) => {
                console.log(data);
                this.makeServicesChart(data);
            });

        // this.makeChart({"types": {"1": 88, "4": 1, "5": 2}, "1": {"TP-LINK": 61, "ZyXEL": 17, "Asus": 7, "D-LINK": 3}, "4": {"Apache": 1}});
    }

    run()
    {
        this.getStatistics();
    }

    makeServicesChart(data)
    {
        console.log(data);
        
        let types = Object.keys(data.types).map((key) => { return {name: EServiceType[key], y: data.types[key]} });
        console.log(types)

        let mainChart = Highcharts.chart('xxx', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Services'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                },
                series: {
                    events: {
                        click: (e) => { this.makeVendorsChart(data, e.point.name) }
                    }
                }
            },
            series: [{
                name: 'Services',
                data: types
            }]
        });
    }

    makeVendorsChart(data, typeName)
    {

        let item = Object.keys(EServiceType).filter((k) => {
            return EServiceType[k] === typeName;
        });

        if (!item.length)
        {
            console.error("No data");
            return;
        }

        let type = item[0];


        let vendors = Object.keys(data[type]).map((vendor) => { return {name: vendor, y: data[type][vendor]} });

        console.log("vendors", vendors)

        let mainChart = Highcharts.chart('zzz', {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Vendors'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                },
                series: {
                    events: {
                        click: (e) => { console.log(e.point.name) }
                    }
                }
            },
            series: [{
                name: 'Vendors',
                data: vendors
            }]
        });
    }
}


$(() => {
    let report = new CScanner();
    report.run();
});
