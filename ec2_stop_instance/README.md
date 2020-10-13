# Hyperglance - ec2_stop_instance

This configuration deploys a lambda that stops EC2 Instances based on Hyperglance Rules.

## Dry Run

By default, the function will stop all instances identified in the rule, if you would like to test the action before update line 32 of the hyperglance_ec2_stop_instance.js [file](https://github.com/hyperglance/aws-rule-automations/blob/master/files/hyperglance_ec2_stop_instance.js#L32)

DryRun Enabled:

```javascript
DryRun: true,
```

DryRun Diabled:

```javascript
DryRun: false,
```

Once you have configured the DryRun mode, deploy the function using:

```terraform
$ terraform init
$ terraform apply
```
