import java.net.*;
import java.io.*;



public class Talk {  
	// define client socket
	private Socket socket = null;
	//define server socket
	private ServerSocket server = null;
    //define bufferedReaders
	private BufferedReader con;
	//define socket input
	private BufferedReader in;
    //define output stream
	private PrintWriter out;
	private String[] sender = {"Client", "Server"};
	private String name;
	private int port = 12987;
//	private InetAddress ia = InetAddress.getLocalHost();
//	private String address = ia.getHostAddress();
	private String address = "localhost";
	
	//constructor
	public Talk(String args[]){
		//chooses which mode to take
		try {
			//for(int i = 0; i < args.length; i++) {
			switch(args[0]) {
				case "-h":
					System.out.println("-h");
					h();
					
				case "-s":
					System.out.println("-s");
					s();
				case "-a":
					System.out.println("-a");
					a();
				case "-help":
					System.out.println("-help");
					help();
			}
			
		}catch(Exception e) {
			System.out.println(e);
		}
	}
	private void status() {
		System.out.printf("Status:\nAddress: %s \nPort: %d", address, port);
	}
	
	
	// acts as client, looks for server
	private void h(){
		try {
			socket = new Socket(address, port);
			//Sender's nametag
			name = sender[1];
			messageHandling();
		}catch(Exception x){
			System.out.println("Client unable to communicate with server");
			System.out.println(x);
		}
	}

	//server method
	private void s() {
		try {
			server = new ServerSocket(port);
			socket = server.accept();
			// lets user know client has connected
			System.out.println("Client connected");
			//Sender's nametag
			name = sender[0];
			messageHandling();
		}catch(Exception r) {
			System.out.println("“Server unable to listen on specified port");
			System.out.println(r);
		}
	}
	
	//looks for server, if no server found, it becomes server
	private void a(){
		try {
			socket = new Socket(address, port);
		}catch(Exception x){
			System.out.println("Client unable to communicate with server");
		}finally{
			s();
		}

	}
	//tells user how to use program
	private void help(){
		System.out.println("\nThis program opens a socket and, based on the mode given, acts as a server or a client.\n Author: A\n Modes:\n  -h: runs the program as a client and looks for server.\n  -s: runs the program as a server and looks for client.\n  -a: runs the program as a client and looks for a server but if no server is found, it switches to act as a server.\n");
	}
	//method to handle all messages
	private void messageHandling() {
		try {
			// gets input from console 
            con = new BufferedReader(new InputStreamReader(System.in));
            
            //gets input from ServerSocket
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
         
            //sends output to socket
            out = new PrintWriter(socket.getOutputStream(), true);
            
            // start signal
         	System.out.println("Connected");
		}catch(Exception c) {
			System.out.println(c);
		}
		
		//Input and Output strings
		String console = " ", fromServer = " ";
		
		
		try {
			//Writes to server
		    while(true){
				while(con.ready() == true){
					//System.out.println(console);
				    //STATUS
					if(console.equals("STATUS")) {
						status();
						console = con.readLine();
					}else {
						console = con.readLine();
						out.println(console);
						//System.out.println("client:" + console);
						//System.out.println("server: " + (fromServer = in.readLine()));
					}
			}
				
				while(in.ready() == true){	
					fromServer = in.readLine();
					System.out.println(name + ": " + fromServer);
					// if (fromServer.equals("oVER")) {
			    	//     System.out.println("Disconnected from Server");
				}	// 	break;}
			}
		}catch(IOException d) {
			System.out.println(d);
		}
			
	}
		
		
		
		
//		try {
//			socket = new Socket(address, port);
//            System.out.println("Connected");
//            
//            //gets input from console
//            System.out.println("eNTER SOEMTHING!!"); 
//            br = new BufferedReader(new InputStreamReader(System.in));
//            
//            //sends output to socket
//            out = new DataOutputStream(socket.getOutputStream());
//		
//		}
//		// Tests for ip address
//		catch(UnknownHostException u) {
//			System.out.println(u); 
//		}
//		//Tests for failed input or output operation
//		catch(IOException i) {
//			System.out.println(i);
//		}
//		// string to read message from input
//		String line = "";
//		
//		// keep reading until "over" is input
//		while (!line.equals("over")) {
//			try {
//				line = br.readLine();
//				out.writeUTF(line);
//			}
//			catch(IOException i) {
//				System.out.println(i);
//			}
//		}
//		//close connection
//		try
//		{
//			br.close();
//			out.close();
//			socket.close();
//		}
//		catch(IOException i) {
//			System.out.println(i);
//		}
//	}


 public static void main(String args[]) {
	//System.out.println("HELLLLLLOOOOOOOOO");
    new Talk(args);
 }
}