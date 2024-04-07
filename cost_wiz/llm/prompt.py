def get_prompt(data, instance):

    cost_optimized_json_example_format = {
        "CurrentInstance": {
            "Instance": "t3.large",
            "CostPerHour": 0.0832,
            "Performance": "The t3.large instance provides 2 vCPUs and 8 GiB memory, which seems sufficient for the workload based on the provided dataset. However, there are periods of low utilization where a smaller instance might be more cost-effective."},
        "SuggestedInstances": [
            {
                "Instance": "t3.medium",
                "Reason": "Based on the provided data, the t3.large instance seems to be underutilized most of the time. The t3.medium instance can be useful for such scenario at a slightly lower cost, which can better handle these kinds of occasional spikes in CPU utilization and memeory usage with better performance.",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0832,
                    "SuggestedCostPerHour": 0.0416,
                    "DifferenceCostPerHour": 0.0416,
                },
            },
            {
                "Instance": "t3.small",
                "Reason": "The t3.small instance provides same number of vCPUs with less memory as compared to the t3.large, which can handle higher CPU utilization spikes more comfortably. The cost is lowered.",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0832,
                    "SuggestedCostPerHour": 0.0208,
                    "DifferenceCostPerHour": 0.0624,
                },
            },
        ],
    }

    upgraded_json_example_format = {
        "CurrentInstance": {"Instance": "t2.nano",
                            "CostPerHour": 0.0058,
                            "Performance": "The t3.micro instance provides 2 vCPUs and 1 GiB of memory, which seems sufficient for the provided dataset based on the average CPU and memory usage."},
        "SuggestedInstances": [
            {
                "Instance": "t2.micro",
                "Reason": "Based on the provided data, the t3.nano instance seems to be overutilized most of the time. The t3.micro instance can be useful for such scenario at a slightly more cost, which can better handle these kinds of spikes in CPU utilization and memeory usage with better performance.",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0058,
                    "SuggestedCostPerHour": 0.0116,
                    "DifferenceCostPerHour": 0.0058,
                },
            },
            {
                "Instance": "t2.small",
                "Reason": "A more better suggestion would be the t3.small instance provides same number of vCPUs with more memory as compared to the t3.nano, which can handle higher CPU utilization spikes more comfortably. The cost is however more than the current one..",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0058,
                    "SuggestedCostPerHour": 0.0230,
                    "DifferenceCostPerHour": 0.0172,
                },
            },
        ],
    }
    return f"""
            You are provided with a dataset encapsulated within <data> tags, which includes time series data organized in columns. Information about the Amazon EC2 instance type used to generate this dataset is enclosed within <instance> tags. Your primary objective is to analyze this dataset, focusing specifically on the efficiency and cost-effectiveness of the employed EC2 instance type.

            Your analysis should:
            
            1. Evaluate the dataset to understand its demands and resource usage.
            2. Compare the current EC2 instance type against available options, considering both cost and performance.
            3. Recommend at least two alternative EC2 instance types that either reduce costs without sacrificing performance or enhance performance if the current instance is underperforming, even if at a higher cost.
            4. Justify the continuation of the current EC2 instance type if it is deemed the most suitable option in terms of cost-efficiency and performance.
            
            Please format your recommendations only as a JSON object, similar to the provided examples. Your JSON output should include:
            
            - The current EC2 instance type, its cost per hour, and details about its performance.
            - At least two suggested EC2 instance types with rationale for each suggestion, including a comparison of cost per hour and performance impact.
            
            An example format for cost-optimized recommendations is shown within <cost_optimized_json_example_format> tags, and an example for suggesting an upgrade due to performance needs is within <upgraded_json_example_format> tags. Replace placeholder values with specific details from your analysis.
            
            Ensure your suggestions aim for cost optimization and address the dataset's requirements effectively.
            
            <cost_optimized_json_example_format>
            {{
              "CurrentInstance": {{
                "Instance": "{cost_optimized_json_example_format["CurrentInstance"]["Instance"]}",
                "CostPerHour": {cost_optimized_json_example_format["CurrentInstance"]["CostPerHour"]}
                "Performance": {cost_optimized_json_example_format["CurrentInstance"]["Performance"]}
              }},
              "SuggestedInstances": [
                {{
                  "Instance": "{cost_optimized_json_example_format["SuggestedInstances"][0]["Instance"]}",
                  "Reason": "{cost_optimized_json_example_format["SuggestedInstances"][0]["Reason"]}",
                  "CostDifferenceCostPerHour": {{
                    "CurrentCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["CurrentCostPerHour"]},
                    "SuggestedCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["SuggestedCostPerHour"]},
                    "DifferenceCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["DifferenceCostPerHour"]}
                  }}
                }},
                {{
                  "Instance": "{cost_optimized_json_example_format["SuggestedInstances"][1]["Instance"]}",
                  "Reason": "{cost_optimized_json_example_format["SuggestedInstances"][1]["Reason"]}",
                  "CostDifferenceCostPerHour": {{
                    "CurrentCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["CurrentCostPerHour"]},
                    "SuggestedCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["SuggestedCostPerHour"]},
                    "DifferenceCostPerHour": {cost_optimized_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["DifferenceCostPerHour"]}
                  }}
                }}
              ]
            }}
            </cost_optimized_json_example_format>
            
            <upgraded_json_example_format>
            {{
              "CurrentInstance": {{
                "Instance": "{upgraded_json_example_format["CurrentInstance"]["Instance"]}",
                "CostPerHour": {upgraded_json_example_format["CurrentInstance"]["CostPerHour"]},
                "Performance": {cost_optimized_json_example_format["CurrentInstance"]["Performance"]}
              }},
              "SuggestedInstances": [
                {{
                  "Instance": "{upgraded_json_example_format["SuggestedInstances"][0]["Instance"]}",
                  "Reason": "{upgraded_json_example_format["SuggestedInstances"][0]["Reason"]}",
                  "CostDifferenceCostPerHour": {{
                    "CurrentCostPerHour": {upgraded_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["CurrentCostPerHour"]},
                    "SuggestedCostPerHour": {upgraded_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["SuggestedCostPerHour"]},
                    "DifferenceCostPerHour": {upgraded_json_example_format["SuggestedInstances"][0]["CostDifferenceCostPerHour"]["DifferenceCostPerHour"]}
                  }}
                }},
                {{
                  "Instance": "{upgraded_json_example_format["SuggestedInstances"][1]["Instance"]}",
                  "Reason": "{upgraded_json_example_format["SuggestedInstances"][1]["Reason"]}",
                  "CostDifferenceCostPerHour": {{
                    "CurrentCostPerHour": {upgraded_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["CurrentCostPerHour"]},
                    "SuggestedCostPerHour": {upgraded_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["SuggestedCostPerHour"]},
                    "DifferenceCostPerHour": {upgraded_json_example_format["SuggestedInstances"][1]["CostDifferenceCostPerHour"]["DifferenceCostPerHour"]}
                  }}
                }}
              ]
            }}
            </upgraded_json_example_format>
            
            <data>
            {data}
            </data>
            
            <instance>
            {instance}
            </instance>
            
            Focus on making recommendations that are both cost-optimized and suitable for the dataset's needs.

            """
