def get_prompt(columns, data, instance):

    example_json = {
        "CurrentInstance": {"Instance": "t3.nano", "CostPerHour": 0.345},
        "SuggestedInstances": [
            {
                "Instance": "t3.nano",
                "Reason": "Based on the provided CPU utilization data, the t3.nano instance seems to be underutilized most of the time. The t3.micro instance offers more vCPUs and memory at a slightly higher cost, which can better handle the occasional spikes in CPU utilization.",
                "CostDifferenceCostPerHour": {
                    "CurrentCostPerHour": 0.0052,
                    "SuggestedCostPerHour": 0.0104,
                    "DifferenceCostPerHour": 0.0052,
                },
            },
            {
                "Instance": "t3.small",
                "Reason": "The t3.small instance provides even more vCPUs and memory compared to the t3.micro, which can handle higher CPU utilization spikes more comfortably. However, the cost is also higher.",
                "CostDifferencePerHour": {
                    "CurrentCostPerHour": 0.0052,
                    "SuggestedCostPerHour": 0.0208,
                    "DifferenceCostPerHour": 0.0156,
                },
            },
        ],
    }
    return f"""
            The dataset you will be working with is framed within <data> tags, featuring time series data structured into columns: {columns}. 
            
            Additionally, details regarding the EC2 instance type that was employed to generate this dataset are encapsulated within <instance> tags.

            Your task is to conduct a comprehensive analysis of the provided datasets, with a specific focus on evaluating the array of available EC2 instance types. 
            
            This analysis should aim to identify a more cost-effective EC2 instance type that could serve as an optimized solution. 
            
            In instances where the current EC2 instance type is deemed to be performing at an optimal level of efficiency, it is recommended to endorse the continuation of its use, justifying that the present EC2 instance type remains the most suited for the task.

            Please ensure to recommend a minimum of two alternative EC2 instance types. Your recommendations should be presented in a strict JSON only format, as illustrated within the <json_example_format> tags provided below.             

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
