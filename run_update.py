import subprocess


try:

    print("\nSTEP 1: Updating SBA data")
    subprocess.run(
        ["python", "update_sba_data.py"],
        check=True
    )


    print("\nSTEP 2: Cleaning SBA data")
    subprocess.run(
        ["python", "clean_sba_data.py"],
        check=True
    )


    print("\nSTEP 3: Creating JSON")
    subprocess.run(
        ["python", "create_json.py"],
        check=True
    )


    print("\nAll SBA updates completed successfully!")


except subprocess.CalledProcessError:
    print("\nUpdate failed.")