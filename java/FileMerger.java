import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.channels.FileChannel;

public class FileMerger {
  public static long runTime(long startTime) {
    return System.currentTimeMillis() - startTime;
  }
  public static void main(String[] args) {
    if (args == null || args.length < 2) {
      System.out.println("Usage: java Main [path of file to be merged] [path of target file]");
      System.exit(1);
    }
    
    long seekPosition = 0;
    
    File filesPath = new File(args[0]);
    File targetFile = new File(args[1]);
    
    if (filesPath.isDirectory()) {
      File[] fileList = filesPath.listFiles();
      long startTime = System.currentTimeMillis();
    
      Thread[] threads = new Thread[10];
      for (int i = 0; i < fileList.length; i++) {
        WriteFile writeFile = new WriteFile(fileList[i], targetFile, seekPosition);
        try {
          seekPosition += writeFile.sourceFileChannel.size();
        } catch (IOException e) {
          e.printStackTrace();
        }
        threads[i] = new Thread(writeFile);
      }
      for (Thread thread: threads) {
        thread.start();
      }
      for (Thread thread: threads) {
        try {
          thread.join();
        } catch(InterruptedException e) {
          e.printStackTrace();
        }
      }
     
      System.out.println("Running Time: " + runTime(startTime));
    } else {
      System.out.println("Please specify the path of file to be merged which is a directory.");
    }
  }
}

class WriteFile implements Runnable {
  public int bufferSize;
  public long seekPosition;
  
  public RandomAccessFile sourceFile;
  public FileChannel sourceFileChannel;
  public RandomAccessFile targetFile;
  public FileChannel targetFileChannel;

  public WriteFile(File sourceFile, File targetFile, long seekPosition) {
    this.seekPosition = seekPosition;

    try {
      this.sourceFile = new RandomAccessFile(sourceFile.getAbsolutePath(), "r");
      this.sourceFileChannel = this.sourceFile.getChannel();
      this.targetFile = new RandomAccessFile(targetFile.getAbsolutePath(), "rw");
      this.targetFileChannel = this.targetFile.getChannel().position(this.seekPosition);
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
  
  @Override
  public void run() {
    try {
        System.out.println("Thread: " + Thread.currentThread() + ", Offset: " + this.seekPosition + ", Size: " + this.sourceFileChannel.size());
        this.sourceFileChannel.transferTo(0, this.sourceFileChannel.size(), this.targetFileChannel);
    } catch (IOException e) {
      e.printStackTrace();
    } finally {
      try {
        this.sourceFile.close();
      } catch(IOException e) {
        e.printStackTrace();
      }
    }
  }
}
