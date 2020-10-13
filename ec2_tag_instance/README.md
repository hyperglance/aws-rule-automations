# Hyperglance - ec2_tag_instance

This configuration deploys a lambda that tags EC2 Instances based on Hyperglance Rules.

## Tag Configuration

By default, the configuration uses the following tags:

```json
  {
    Key: 'HyperglanceTest', 
    Value: 'HyperglanceTest'
  },
  {
    Key: 'Description',
    Value: 'Tag Added By Hyperglance'
  },
  {
    Key: 'Your Tag',
    Value: 'Your Value'
  }
```

To modify these to your, requirements edit the hyperglance_ec2_tag_instance.js [file](https://github.com/hyperglance/aws-rule-automations/blob/master/files/hyperglance_ec2_tag_instance.js) The tag definition starts on line [33](https://github.com/hyperglance/aws-rule-automations/blob/master/files/hyperglance_ec2_tag_instance.js#L33).

Update and add any additional tags you require, each key/value pairs is surrounded by `{ }` and each pair is separated by a comma `,`

The all of the tags sit within the `Tags: [ ]` block:

```json
  Tags: [
    {
      Key: 'Your Tag 1', 
      Value: 'Your Value 1'
    },
    {
      Key: 'Description',
      Value: 'Host Has Egress Internet'
    },
    {
      Key: 'Tagged By',
      Value: 'Hyperglance'
    }
  ]
```

Once the tags have been updated to you liking, deploy the function using:

```terraform
$ terraform init
$ terraform apply
```