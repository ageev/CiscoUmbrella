# Umbrella test URLs https://support.umbrella.com/hc/en-us/articles/230903728-How-To-Successfully-test-to-ensure-you-re-running-Umbrella-correctly
$urls = 'www.internetbadguys.com',
        'www.examplemalwaredomain.com',
        'malware.opendns.com',
        'www.examplebotnetdomain.com',
        'www.exampleadultsite.com'

foreach ($url in $urls){
        Resolve-DnsName -Name $url
        }
