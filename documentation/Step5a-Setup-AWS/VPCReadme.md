**Create a VPC using the wizard in AWS**

In this task, we want to create an Amazon Virtual Private Cloud (VPC), which is a logically isolated virtual network in your AWS account. This VPC will have 1 public subnet, 1 private subnet, and one Network Address Translation (NAT) Gateway, which will be used to deploy AWS CDK.

1. Access the AWS Management Console, select **Services**. at the top of the screen, and select the **VPC** service. **Or**, you can type **vpc** in the search box to the right of **Services**, then select VPC from the list that comes up.
2. Check to make sure you're still in the correct region for your labs, by checking the region name at the top right of the AWS Console, such as the North Virginia region, us-east-1.
3. Select **VPC Dashboard** at the top of the lefthand pane.
4. Click **Create VPC**.
            1. Make sure that VPC and more is selected.
            2. Under the Name tag auto-generation field enter your initials followed by -cdk. Because Auto-generate is checked, this will name your VPC something like de-cdk-vpc (assuming your initials are "de"), and all other related resources such as subnets, route tables, internet gateway, and public NAT gateway.
            3. For Number of Availability Zones select 1 so that we will use 1 AZ for our VPC. 


