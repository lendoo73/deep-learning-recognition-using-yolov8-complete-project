# [Deploy on AWS with Fargate](https://aws.github.io/copilot-cli/docs/getting-started/first-app-tutorial/)

## Prerequisit

```shell
aws --version
docker --version
copilot --version
```

## Set up AWS Credentials

```shell
aws configure
```

You'll be prompted for:
* AWS Access Key ID
* AWS Secret Access Key
* Region (e.g., eu-west-2)
* Output format (e.g., json)

## Permissions for IAM User to deploy with Fargate

(Create an inline policy)

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"iam:PassRole",
				"ecs:*",
				"elasticloadbalancing:*",
				"cloudformation:*",
				"logs:*",
				"s3:*",
				"ecr:*",
				"route53:*",
				"lambda:*",
				"ssm:GetParameter",
				"ssm:PutParameter",
				"ssm:AddTagsToResource",
				"ssm:GetParametersByPath",
				"ssm:DeleteParameter",
				"sts:AssumeRole",
				"tag:GetResources",
				"iam:PassRole",
				"iam:GetRole",
				"iam:DeleteRolePolicy",
				"iam:CreateRole",
				"iam:DeleteRole",
				"iam:PutRolePolicy",
				"iam:TagRole",
				"iam:TagPolicy",
				"iam:ListRoles",
				"iam:ListPolicies",
				"iam:ListAttachedUserPolicies",
				"ecr:CreateRepository",
				"kms:*",
				"cloudwatch:*"
			],
			"Resource": "*"
		}
	]
}
```

## Deploying

```shell
copilot init
```
Example inputs when prompted:
* Application name: `ml-rest-api`
* Service name:     `machine-learning-rest-api`
* Select the Dockerfile you want to use.
* Choose **Load Balanced Web Service**.
* Environment name: `test`

Or use flags to run non-interactively:
```shell
copilot init \
  --app ml-rest-api \
  --name machine-learning-rest-api \
  --dockerfile ./Dockerfile \
  --type "Load Balanced Web Service" \
  --env test \
  --deploy
```


Edit `copilot/machine-learning-rest-api/manifest.yml`

```yaml
cpu: 1024
memory: 2048
```

Redeploying the Service:
```shell
copilot svc deploy --name machine-learning-rest-api --env test
```

## Update Existing Deployment

1. Build a new release: `npm run build`
2. Update the existing deployment: `copilot svc deploy --name machine-learning-rest-api --env test`

**Note**: Service name and environment name must match those used during the initial deployment.

## Clean Up

```shell
copilot app delete
```

To run with the admin user: `AWS_PROFILE=admin copilot app delete`

Or set the profile for the session:
```shell
export AWS_PROFILE=admin
copilot app delete
```

### CLI Commands for Quick Checks (to verify everything has been deleted)

```shell
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE
aws ecr describe-repositories
aws s3 ls
aws iam list-roles | grep machine-learning-rest-api
```

## Troubleshooting

```shell
copilot svc logs --follow

copilot svc show --name machine-learning-rest-api

```
