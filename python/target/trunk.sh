rm -rf report
mkdir report
cd trunk/360Video
cp -r /opt/zygote/360Video/trunk/* ./
sed -i 's/\\\\/\//g' project.properties
python changeLog.py ${needProguard} ${needLog}

if [ -e ../../replace_file ]
then
	mv ../../replace_file ./${replace_file}
    unzip -o ${replace_file}
    rm ${replace_file}
fi


if [ "${isClone}" = "true" ]; then 
	/opt/zygote/python/make_clone.py /opt/zygote/python/make_clone_config.json
	mv ant.properties.clone ant.properties;
    mv project.properties.clone project.properties
else 
	cp AndroidManifest.xml AndroidManifest_clone.xml
	mv ant.properties.normal ant.properties;
fi

./genbuild.sh

#ant clean
#ant build

if [ "${isClone}" = "true" ]; then 
	cd build
    for x in `ls`; do /opt/zygote/360Video/utils/jiagu.py $x; done
    cd -
fi
