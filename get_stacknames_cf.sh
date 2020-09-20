alias jq='/c/Users/vkarth546/Downloads/jq-win64.exe'
app_tpages=$(cf curl v2/apps | jq '.total_pages')
space_tpages=$(cf curl v2/spaces | jq '.total_pages')
stack_tpages=$(cf curl v2/stacks | jq '.total_pages')
echo $app_tpages
echo $space_tpages
echo $stack_tpages
echo "App_Name,Stack_Name,Space_Name" > all_apps.csv
for i in $(seq 1 $app_tpages)
do
cf curl /v2/apps?page=${i} | jq '.resources[] | .entity.name + "," + .entity.stack_url + "," + .entity.space_url' >> all_apps.csv
done

for i in $(seq 1 $stack_tpages)
do
cf curl /v2/stacks?page=${i} | jq '.resources[] | .metadata.url + "," + .entity.name' >> all_stacks.csv
done

for i in $(seq 1 $space_tpages)
do
cf curl /v2/spaces?page=${i} | jq '.resources[] | .metadata.url + "," + .entity.name' >> all_spaces.csv
done

sed -i "s#\"##g" all_apps.csv
sed -i "s#\"##g" all_stacks.csv
sed -i "s#\"##g" all_spaces.csv

export IFS=","
cat all_spaces.csv | while read url name
do
sed -i "s#${url}#${name}#g" all_apps.csv
done

cat all_stacks.csv | while read url name
do
sed -i "s#${url}#${name}#g" all_apps.csv
done
rm -rf all_stacks.csv all_spaces.csv
echo "All application with stacks and spaces are generated"

