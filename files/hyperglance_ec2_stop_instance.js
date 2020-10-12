const AWS = require('aws-sdk');

exports.handler = async (event) => {
    const hgAlert = JSON.parse(event.Records[0].Sns.Message);
    
    console.log(
        'Received Hyperglance alert from saved-search.\n',
        '( ',
        'Name: ', hgAlert.name, '\n',
        'Pack: ', hgAlert.pack, '\n',
        'Description: ', hgAlert.description, '\n',
        'Status: ', hgAlert.status, '\n',
        'Threshold: ', hgAlert.threshold, '\n',
        'Evaluation Time: ', hgAlert.evaluatedAt, '\n',
        'Num Results: ', hgAlert.results.length,
        ' )'
    );
    
    // we only care about threshold breaches
    if (hgAlert.status !== 'ABOVE_THRESHOLD' &&
        hgAlert.status !== 'BELOW_THRESHOLD') {
            console.log('Status was ', hgAlert.status, ', so exiting with nothing to do');
            return;
    }
    
    await processEachRegion(hgAlert, async (region, resourceIDs) => {
        const EC2 = new AWS.EC2({apiVersion: '2016-11-15', region});
        // STOP INSTANCE
        const stopInstanceParams = {
            InstanceIds: resourceIDs,
            // Set this to true to 'test' the action without actually performing it
            DryRun: false,
            /* Forces the instances to stop. The instances do not have an opportunity to flush file system caches or file system metadata. 
            If you use this option, you must perform file system check and repair procedures. 
            This option is not recommended for Windows instances.*/
            Force: false 
        };
        // Stop the Instances
        await EC2.stopInstances(stopInstanceParams).promise();
    });
};

async function processEachRegion(hgAlert, callback) {
    // group resource IDs up according to their region
    const resourcesByRegion = hgAlert.results.reduce(
        (map, res) => {
            const ids = map.get(res.region) || [];
            ids.push(res.id);
            return map.set(res.region, ids);
        }, new Map());
    
    // connect to each region and issue the request
    for (const [region, resourceIDs] of resourcesByRegion.entries()) {
        await callback(region, resourceIDs);
    }
}