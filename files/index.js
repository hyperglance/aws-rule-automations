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
    
        // TAGGING
        /*const tagParams = {
            Resources: resourceIDs,
            Tags: [{Key: 'HyperglanceTest', Value: 'HyperglanceTest'}]
        };
        
        await EC2.createTags(tagParams).promise();*/
        
        // TERMINATION
        const terminateParams = {
            InstanceIds: resourceIDs,
            DryRun: true // set this to true to 'test' the action without actually performing it
        };
        
        await EC2.terminateInstances(terminateParams).promise();
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