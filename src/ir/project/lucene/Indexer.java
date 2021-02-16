package ir.project.lucene;

import java.io.*;
import java.util.List;
import java.util.Set;

import org.apache.lucene.document.*;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.JSONArray;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;


import org.apache.lucene.util.Version;

public class Indexer {

    private IndexWriter writer;

    public Indexer(String indexDirectoryPath) throws IOException {
        //this directory will contain the indexes
        Directory indexDirectory =
                FSDirectory.open((new File(indexDirectoryPath)).toPath());

        StandardAnalyzer analyzer = new StandardAnalyzer();
        IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
        //create the indexer
        iwc.setOpenMode(IndexWriterConfig.OpenMode.CREATE);
        writer = new IndexWriter(indexDirectory, iwc);
    }

    public void close() throws CorruptIndexException, IOException {
        try {
            writer.commit();
        } catch (IOException ex) {
            System.err.println("We had a problem closing the index: " + ex.getMessage());
        }
        writer.close();
    }

    private void indexFile(Reader reader) throws IOException {
        Object fileObjects = JSONValue.parse(reader);
        //Document document = getDocument(file);
        JSONArray arrayObjects = (JSONArray)fileObjects;
        addDocuments(arrayObjects);
    }

    public void addDocuments(JSONArray jsonObjects){
        for(Object object: (List)jsonObjects){
            Document doc = new Document();
            for(Object field : ((JSONObject)object).keySet()){
                if(((JSONObject) object).get((field)) != null && !((JSONObject) object).get((field)).toString().isEmpty()) {
                    Class type = ((JSONObject) object).get(field).getClass();
                    //System.out.println("Here");
                    if (field.toString().equals("tweets")) {
                        doc.add(new TextField((String) field, (String) (((JSONObject) object).get(field)), Field.Store.YES));
                    } else if (field.toString().equals("name")) {
                        doc.add(new TextField((String) field, (String) (((JSONObject) object).get(field)), Field.Store.YES));
                    } else if (field.toString().equals("screen_name")) {
                        doc.add(new StringField((String) field, (String) (((JSONObject) object).get(field)), Field.Store.YES));
                    } else  if(field.toString().equals("location")) {
                        doc.add(new TextField((String) field, (String) (((JSONObject) object).get(field)), Field.Store.YES));
                    } else if (field.toString().equals("description")) {
                        doc.add(new TextField((String) field, (String) (((JSONObject) object).get(field)), Field.Store.YES));
                    } else if (field.toString().equals("followers_count")) {
                        doc.add(new NumericDocValuesField((String) field, (long) (((JSONObject) object).get(field))));
                    } else if (field.toString().equals("likes")) {
                        doc.add(new NumericDocValuesField((String) field, (long) (((JSONObject) object).get(field))));
                    } else if (field.toString().equals("retweets")) {
                        doc.add(new NumericDocValuesField((String) field, (long) (((JSONObject) object).get(field))));
                    } //else if (type.equals(Double.class)) {
                        //doc.add(new DoublePoint((String) field, (double) (((JSONObject) object).get(field))));

                    //} else if (type.equals(Boolean.class)) {
                        //doc.add(new StringField((String) field, (((JSONObject) object).get(field)).toString(), Field.Store.YES));
                    //}
                }
            }
            try {
                writer.addDocument(doc);
            } catch (IOException ex) {
                System.err.println("Error adding documents to the index."  + ex.getMessage());
            }
        }
    }

    public int createIndex(String dataDirPath, FileFilter filter)
            throws IOException {
        //get all files in the data directory
        File[] files = new File(dataDirPath).listFiles();
        for (File file : files) {
            if(!file.isDirectory()
                    && !file.isHidden()
                    && file.exists()
                    && file.canRead()
                    && filter.accept(file)
            ){
                System.out.println("Indexing "+file.getCanonicalPath());
                InputStream jsonFile = new FileInputStream(file);
                Reader readerJson = new InputStreamReader(jsonFile);
                indexFile(readerJson);
            }
        }
        return  writer.getDocStats().numDocs;
    }
}