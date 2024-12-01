<script>
import axios from "axios";

export default {
  data() {
    return {
      isLogin: true,
      username: "",
      email: "",
      firstName: "",
      lastName: "",
      password: "",
      confirmPassword: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:8000/login/", {
          email: this.email,
          password: this.password,
        });
        alert(response.data.message);
      } catch (error) {
        this.error = error.response.data.detail || "Đã xảy ra lỗi.";
      }
    },
    async register() {
      try {
        const checkResponse = await axios.post("http://localhost:8000/check_user/", {
          email: this.email,
          username: this.username,
        });

        if (checkResponse.data.exists) {
          this.error = "Tài khoản hoặc email đã tồn tại.";
          return;
        }

        if (this.password !== this.confirmPassword) {
          this.error = "Mật khẩu xác nhận không khớp.";
          return;
        }

        const response = await axios.post("http://localhost:8000/register/", {
          username: this.username,
          email: this.email,  // Pass email here
          first_name: this.firstName,
          last_name: this.lastName,
          password: this.password,
        });
        alert(response.data.message);
        this.isLogin = true;
      } catch (error) {
        this.error = error.response.data.detail || "Đã xảy ra lỗi.";
      }
    }
  },
};
</script>

<template>
  <div class="relative pt-12 px-4 min-h-screen bg-gray-100">
    <div class="absolute top-0 inset-x-0 h-80 bg-gradient-to-b from-indigo-500 to-indigo-700 -z-10"></div>
    <div class="max-w-md mx-auto p-8 bg-white rounded-lg shadow-lg border border-gray-200">
      <h2 class="text-3xl font-semibold text-center text-indigo-700 mb-6">
        {{ isLogin ? "Đăng Nhập" : "Đăng Ký" }}
      </h2>
      
      <!-- Form -->
      <form @submit.prevent="isLogin ? login() : register()" class="space-y-6">
        <div v-if="!isLogin">
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input
            type="text"
            v-model="username"
            id="username"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="email"
            id="email"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div v-if="!isLogin">
          <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
          <input
            type="text"
            v-model="firstName"
            id="firstName"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <div v-if="!isLogin">
          <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
          <input
            type="text"
            v-model="lastName"
            id="lastName"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            id="password"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <div v-if="!isLogin">
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Xác nhận Mật khẩu</label>
          <input
            type="password"
            v-model="confirmPassword"
            id="confirmPassword"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <button
          type="submit"
          class="w-full py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
        >
          {{ isLogin ? "Đăng Nhập" : "Đăng Ký" }}
        </button>
      </form>
      
      <!-- Thông báo Lỗi -->
      <div v-if="error" class="text-red-500 text-sm mt-4">{{ error }}</div>
      
      <!-- Liên kết Chuyển đổi -->
      <div class="text-center mt-6">
        <a
          href="#"
          class="text-indigo-600 hover:text-indigo-800 text-sm"
          @click.prevent="isLogin = !isLogin"
        >
          {{ isLogin ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập" }}
        </a>
      </div>
    </div>
  </div>
</template>

