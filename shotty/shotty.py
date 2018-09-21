import boto3
import click
#import sys

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.group()
def instances():
	"""Commands for instances"""

@instances.command('list')
#@click.command()
@click.option('--project', default=None, help="Only instances for project (tag project:<name>)")
def list_instances(project):
	"List EC2 instances"
	instances = []

	if project:
		filters = [{'Name':'tag:Name', 'Values':["tag:TE"]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		ec2.instances.all()
		
	for i in ec2.instances.all():
#	for i in instances:
#		tags = { t['Key']: t['Value'] for t in i.tags or [] }
					
		print(', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
#			tags.get('Name', '<no Project>')
			)))
  
#	return
@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag project:<name>)")
def stop_instances(project):
	"Stop EC2 instances"

	instances = []

	if project:
		filters = [{'Name':'tag:Name', 'Values':["tag:TE"]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		ec2.instances.all()
	
	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()
	return	
if __name__ == '__main__':
# print(sys.argv)
# list_instances()
  instances()
