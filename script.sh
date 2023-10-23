working_directory=$(pwd)
hadoop_directory=/google_page_rank
jar_path=/home/devansh/hadoop-3.2.3/share/hadoop/tools/lib/hadoop-streaming-3.2.3.jar

# downloading the dataset
mkdir ./dataset
wget https://snap.stanford.edu/data/web-Google.txt.gz
gunzip -c ./web-Google.txt.gz > ./dataset/web-google.txt
rm ./web-Google.txt.gz


# taking number of nodes, tolerance, value of beta as input from user
echo "Enter Number of nodes in the graph (At no input, Default = 875713): "
read user_input
if [ -z $user_input ]; then
	num=875713
else
    num=$user_input
fi

echo "Enter Value of Tolerance (At no input, Default = 1e-8): "
read user_input
if [ -z $user_input ]; then
	tolerance=1e-8
else
    tolerance=$user_input
fi

echo "Enter Value of Beta (At no input, Default = 0.85): "
read user_input
if [ -z $user_input ]; then
	beta=0.85
else
    beta=$user_input
fi


# for storing the outputs of each iteration
mkdir ./output
mkdir ./output/scores
mkdir ./output/difference

hadoop fs -mkdir $hadoop_directory
hadoop fs -copyFromLocal $working_directory/dataset/web-google.txt $hadoop_directory/web-google.txt

############################################ Page Rank Algorithm #############################333#####################

# initialize
hadoop jar $jar_path -input $hadoop_directory/web-google.txt -output $hadoop_directory/degree -mapper "python3 $working_directory/src/init.py degree_mapper" -reducer "python3 $working_directory/src/init.py degree_reducer"
hadoop jar $jar_path -input $hadoop_directory/web-google.txt -output $hadoop_directory/score0 -mapper "python3 $working_directory/src/init.py score_mapper" -reducer "python3 $working_directory/src/init.py score_reducer $num"
hadoop jar $jar_path -input $hadoop_directory/web-google.txt -output $hadoop_directory/edges -mapper "python3 $working_directory/src/init.py edge_mapper" -reducer "python3 $working_directory/src/init.py edge_reducer"

# loop
counter=1
difference=1000000
threshold=$( python3 -c "print($num * float($tolerance))")

while [[ "$( python3 -c "print($difference > $threshold)")" == "True" ]]; do

    counter_minus_one=$((counter - 1))

    # compute
    hadoop jar $jar_path -input $hadoop_directory/score$counter_minus_one/part-00000,$hadoop_directory/degree/part-00000,$hadoop_directory/edges/part-00000 -output $hadoop_directory/combined -mapper /bin/cat -reducer "python3 $working_directory/src/compute.py combine_reducer $beta"
    hadoop jar $jar_path -input $hadoop_directory/combined/part-00000 -output $hadoop_directory/added -mapper "python3 $working_directory/src/compute.py add_mapper" -reducer  "python3 $working_directory/src/compute.py add_reducer $num" 

    # output for next loop
    hadoop jar $jar_path -input $hadoop_directory/added/part-00000,$hadoop_directory/score$counter_minus_one/part-00000 -output $hadoop_directory/score$counter -mapper /bin/cat -reducer "python3 $working_directory/src/compute.py score_reducer" 

    # final output to be saved
    hadoop jar $jar_path -input $hadoop_directory/added/part-00000,$hadoop_directory/web-google.txt -output $hadoop_directory/iter$counter -mapper "python3 $working_directory/src/final.py final_mapper" -reducer "python3 $working_directory/src/final.py final_reducer $num"
    hadoop fs -copyToLocal $hadoop_directory/iter$counter/part-00000 $working_directory/output/scores/iter$counter.txt

    
    if [ $counter -gt 1 ]; then

    	# difference with previous iteration
    	hadoop jar $jar_path -input $hadoop_directory/iter$counter/part-00000 -output $hadoop_directory/inter -mapper "python3 $working_directory/src/difference.py diff_mapper"  -reducer /bin/cat
        hadoop jar $jar_path -input $hadoop_directory/inter/part-00000,$hadoop_directory/iter$counter_minus_one/part-00000  -output $hadoop_directory/diff$counter -mapper /bin/cat -reducer "python3 $working_directory/src/difference.py diff_reducer"

        hadoop fs -copyToLocal $hadoop_directory/diff$counter/part-00000 $working_directory/output/difference/diff$counter.txt
        read difference < $working_directory/output/difference/diff$counter.txt

    	# deleting unnecessary outputs
        hadoop fs -rm -r $hadoop_directory/inter
        hadoop fs -rm -r $hadoop_directory/iter$counter_minus_one
        hadoop fs -rm -r $hadoop_directory/diff$counter

    fi

    # deleting unnecessary outputs
    hadoop fs -rm -r $hadoop_directory/combined
    hadoop fs -rm -r $hadoop_directory/added
    hadoop fs -rm -r $hadoop_directory/score$counter_minus_one

    counter=$((counter + 1))

done

# storing the plot of convergence
mkdir ./results
pip install matplotlib
python3 ./result.py $threshold
