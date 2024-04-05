def get_prompt():
    columns = f"""timestamp,Average_CPUUtilization,Maximum_CPUUtilization,Minimum_CPUUtilization"""
    data = f"""
                timestamp,Average_CPUUtilization,Maximum_CPUUtilization,Minimum_CPUUtilization
                2024-03-10,0.2393241832,0.5084095948,0.2083472231
                2024-03-11,0.2198618488,0.2499333511,0.1999533442
                2024-03-12,0.2630860413,2.760357596,0.1999666722
                2024-03-13,0.2329128924,0.366568915,0.1917145953
                """
    instance = "t3.nano"
    example_json = {
        "CurrentInstance": {
            "Instance": "t3.nano",
            "CostPerHour": 0.345
        },
        "SuggestedInstances": [
            {
                "Instance": "t3.nano",
                "Reason": "Based on the provided CPU utilization data, the t3.nano instance seems to be underutilized most of the time. The t3.micro instance offers more vCPUs and memory at a slightly higher cost, which can better handle the occasional spikes in CPU utilization.",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0052,
                    "SuggestedCostPerHour": 0.0104,
                    "DifferenceCostPerHour": 0.0052
                }
            },
            {
                "Instance": "t3.small",
                "Reason": "The t3.small instance provides even more vCPUs and memory compared to the t3.micro, which can handle higher CPU utilization spikes more comfortably. However, the cost is also higher.",
                "CostDifferencePerHour": {
                    "CurrentCostPerHour": 0.0052,
                    "SuggestedCostPerHour": 0.0208,
                    "DifferenceCostPerHour": 0.0156
                }
            }
        ]
    }
    prompt = f"""
                You will receive time series data with columns {columns} enclosed within the <data> tags. 
                Additionally, within the <instance> tags, you'll find the type of instance used to generate this time series data.

                Your objective is to analyze these values and recommend a more cost-effective EC2 instance type for optimization.

                Please provide at least two EC2 instance suggestions. The output format should strictly adhere to JSON format. 
                An example of the JSON format is provided within <json_example_format> tags below.

                <json_example_format>
                {{
                  "CurrentInstance": {{
                    "Instance": "{example_json["CurrentInstance"]["Instance"]}",
                    "CostPerHour": {example_json["CurrentInstance"]["CostPerHour"]}
                  }},
                  "SuggestedInstances": [
                    {{
                      "Instance": "{example_json["SuggestedInstances"][0]["Instance"]}",
                      "Reason": "{example_json["SuggestedInstances"][0]["Reason"]}",
                      "CostDifferenceCostPerHour": {{
                        "CurrentCostPerHour": {example_json["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["CurrentCostPerHour"]},
                        "SuggestedCostPerHour": {example_json["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["SuggestedCostPerHour"]},
                        "DifferenceCostPerHour": {example_json["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["DifferenceCostPerHour"]}
                      }}
                    }},
                    {{
                      "Instance": "{example_json["SuggestedInstances"][1]["Instance"]}",
                      "Reason": "{example_json["SuggestedInstances"][1]["Reason"]}",
                      "CostDifferencePerHour": {{
                        "CurrentCostPerHour": {example_json["SuggestedInstances"][1]["CostDifferencePerHour"]["CurrentCostPerHour"]},
                        "SuggestedCostPerHour": {example_json["SuggestedInstances"][1]["CostDifferencePerHour"]["SuggestedCostPerHour"]},
                        "DifferenceCostPerHour": {example_json["SuggestedInstances"][1]["CostDifferencePerHour"]["DifferenceCostPerHour"]}
                      }}
                    }}
                  ]
                }}
                <json_example_format>

                <data>{data}<data>

                <instance>{instance}<instance>

                """
