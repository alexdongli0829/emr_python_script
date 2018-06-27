import boto3    

client = boto3.client('emr', region_name='cn-north-1')

response = client.run_job_flow(
    Name="DDBBackup",
    ReleaseLabel='emr-5.5.0',
    Instances={
        'MasterInstanceType': 'm3.xlarge',
        'SlaveInstanceType': 'm3.xlarge',
        'InstanceCount': 4,
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False,
    },
    Applications=[
        {
            'Name': 'Hive'
        }
    ],
    Steps=[
    {
        'Name': 'Setup Debugging',
        'ActionOnFailure': 'TERMINATE_CLUSTER',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['state-pusher-script']
        }
    },
    {
        'Name': 'DDB backup',
        'ActionOnFailure': 'TERMINATE_CLUSTER',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': ['hive-script','--run-hive-script','--args','-f','s3://dongaws/ddbbackuptest/back.hql']
        }
    }
    ],
    VisibleToAllUsers=True,
    JobFlowRole='EMR_EC2_DefaultRole',
    ServiceRole='EMR_DefaultRole',
    ScaleDownBehavior='TERMINATE_AT_INSTANCE_HOUR'
)
