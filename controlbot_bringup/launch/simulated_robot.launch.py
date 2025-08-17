import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    use_slam = LaunchConfiguration("use_slam")

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="false"
    )

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_1_imu_description"),
            "launch",
            "gazebo.launch.py"
        ),
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_controller"),
            "launch",
            "controller.launch.py"
        ),
        launch_arguments={
            "use_simple_controller": "False",
            "use_python": "False"
        }.items(),
    )
    
    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_controller"),
            "launch",
            "joystick_teleop.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "True"
        }.items()
    )

    localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_localization"),
            "launch",
            "global_localization.launch.py"
        ),
        condition=UnlessCondition(use_slam)
    )
    ekf_odom_filtered = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_localization"),
            "launch",
            "local_localization.launch.py"
        ),
    )
    
    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_mapping"),
            "launch",
            "slam.launch.py"
        ),
        condition=IfCondition(use_slam)
    )


    navigation = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("controlbot_navigation"),
            "launch",
            "navigation.launch.py"
        ),
    )

    


    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
                get_package_share_directory("nav2_bringup"),
                "rviz",
                "nav2_default_view.rviz"
            )
        ],
        output="screen",
        parameters=[{"use_sim_time": True}],
    )
    
    return LaunchDescription([
        use_slam_arg,
        gazebo,
        controller,
        joystick,
        localization,
        slam,
        ekf_odom_filtered,
        navigation,
        rviz
    ])