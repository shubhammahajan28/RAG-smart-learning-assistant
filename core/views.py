from django.shortcuts import render

# Create your views here.
import os
import pandas as pd
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from .rag_loader import load_vectorstore
from .ml_model import analyze_weakness
from .models import StudyRecord
from .serializers import RegisterSerializer

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response({"msg": "Registered successfully"})
        return Response(s.errors, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if not user.check_password(password):
            return Response({"error": "Wrong password"}, status=400)
        token = RefreshToken.for_user(user)
        return Response({"refresh": str(token), "access": str(token.access_token)})
    
class ImportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        csv_path = r"C:\Users\Admin\OneDrive\Desktop\Python Project\llms-ml-project\study-assistant\data\study_user_data.csv"
        if not os.path.exists(csv_path):
            return Response({"error": "data/study_user_data.csv not found"}, status=400)
        df = pd.read_csv(csv_path)
        StudyRecord.objects.all().delete()
        for _, row in df.iterrows():
            StudyRecord.objects.create(
                domain=row["domain"],
                topic=row["topic"],
                correctness=row["correctness"],
                time_spent=row["time_spent"],
                confused=bool(row["confused"]),
            )
        return Response({"msg": f"Loaded {len(df)} study records"})
    
class AnalyzeWeaknessView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        csv_path = r"C:\Users\Admin\OneDrive\Desktop\Python Project\llms-ml-project\study-assistant\data\study_user_data.csv"
        if not os.path.exists(csv_path):
            return Response({"error": "CSV missing"}, status=400)
        weak = analyze_weakness(csv_path)
        return Response({"weak_topics": weak.to_dict(orient="records")})
    
class RAGQueryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        query = request.data.get("query")
        topic = request.data.get("topic")
        if not query:
            return Response({"error": "Missing query"}, status=400)

        db = load_vectorstore()
        retriever = db.as_retriever(search_kwargs={"k": 3})
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, openai_api_key=api_key)
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        prompt = f"Student is studying '{topic}'. Explain clearly: {query}"
        answer = qa.run(prompt)
        return Response({"answer": answer})